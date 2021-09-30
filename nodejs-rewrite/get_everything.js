import fs from 'fs';
import { exec, execSync, spawn } from 'child_process';
import readline from 'readline';
var rl = readline.createInterface(process.stdin, process.stdout);
import util from 'util' 
const question = util.promisify(rl.question).bind(rl);

// Export each team chat to a file

// Export DM's to file

// Export Git Repos to file

async function export_team_memberships(tmp_file_output){
    console.log("running get_team_memberships")
    let team_memberships = [];
    let tmp_raw_string = execSync("keybase team list-memberships").toString("utf8")
    tmp_raw_string.split("\n").slice(1, -1).forEach((element) => {
        let myRegex = element.replace(/  +/g, ' ').split(" ")
        team_memberships.push({
            "Team" : myRegex[0],
            "Role" : myRegex[1],
            "Members": myRegex[2],
        })
    });
    //  console.log(tmp_raw_string)
    //  console.log(team_memberships)
    fs.writeFileSync(tmp_file_output, JSON.stringify(team_memberships), (err) => {
            if (err) {
                throw err;
            }
            console.log(`team_memberships is saved to ${tmp_file_output}.`);
    });
    return team_memberships;
}
// async function get_team_memberships(tmp_file_output){
//     let team_memberships;
//     if (fs.existsSync(tmp_file_output)){
//     }
//     else {
//         export_team_memberships(tmp_file_output)
//     }

//     return team_memberships
// }

async function get_keybase_topic_page(tmp_channel_name, tmp_members_type, tmp_topic_name, tmp_pagiation_next){
    let keybase_topic_messages_cmd_str = {
         "method": "read",
         "params": {
             "options": {
                 "channel": {
                     "name": tmp_channel_name,
                     "members_type": tmp_members_type,
                     "topic_name": tmp_topic_name
                 },
                 "pagination": {
                     "num": 270
                 }
             }
         }
     }
     if (tmp_pagiation_next != undefined) {
         keybase_topic_messages_cmd_str.params.options.pagination.next = tmp_pagiation_next
     }
     let cmd_json_string = JSON.stringify(keybase_topic_messages_cmd_str)
     let command = ["keybase", "chat", "api", "-m", "'"+cmd_json_string+"'"].join(' ')
     // console.log(command)
     let response_object = await JSON.parse(execSync(command).toString("utf8"))
     return response_object
 }

async function get_keybase_topic(tmp_channel_name, tmp_members_type, tmp_topic_name){
    let recursive_messages = await get_keybase_topic_page(tmp_channel_name, tmp_members_type, tmp_topic_name)
    let topic_messages = []
    recursive_messages.result.messages.forEach((message) => {
        topic_messages.push(message)
    })
    while (  !(Object.keys(recursive_messages.result.pagination).indexOf("last") >= 0)  ){
        console.log(recursive_messages)
        recursive_messages = await get_keybase_topic_page(tmp_channel_name, tmp_members_type, tmp_topic_name, recursive_messages.result.pagination.next)
        recursive_messages.result.messages.forEach((message) => {
            topic_messages.push(message)
        })
    }
    return topic_messages
}

async function get_method_list(){
    let cmd_json_string = JSON.stringify({"method": "list"})
    let command = ["keybase", "chat", "api", "-m", "'"+cmd_json_string+"'"].join(' ')
    let response_object = JSON.parse(execSync(command).toString("utf8"))
    return response_object
}

async function get_keybase_user(){
    try {
        let terminal_string = (await execSync("keybase whoami")).toString("utf8")
        console.log(terminal_string.length)
        return terminal_string.substr(0, terminal_string.length - 1)
    } catch (err) {
        console.log(err)
        console.log("You do not have keybase installed")
        console.log("Exiting now")
        process.exit(1)
    }

}

async function create_folder_if_not_exist(create_folder_name){
    if (  fs.existsSync(create_folder_name)  ) {
        console.log(`${create_folder_name} Folder Already Exists`)
    }
    else {
        console.log()
        fs.mkdirSync(create_folder_name)
        console.log(`${create_folder_name} directory created successfully!`);
    }
}


async function setup_folders(export_dir, keybase_user, team_memberships){
    create_folder_if_not_exist(`${export_dir}/${keybase_user}`)
    create_folder_if_not_exist(`${export_dir}/${keybase_user}/teams`)
    for(var i = 0; i < team_memberships.length; i++){
    }

}

async function get_team_topics(export_dir, keybase_user, team_name){
    let topic_file_name = `${export_dir}/${keybase_user}/teams/${team_name}/topics.json`
    if (  fs.existsSync(`${export_dir}/${keybase_user}/teams/${team_name}/topics.json`)  ) {
        return JSON.parse(await fs.readFileSync(topic_file_name, 'utf8'))
    }
    else {
        let team_topics;
        create_folder_if_not_exist(`${export_dir}/${keybase_user}/teams/${team_name}`)
        let keybase_team_topics_cmd_str = {
            "method": "listconvsonname",
            "params": {
                "options": {
                    "topic_type": "CHAT",
                    "members_type": "team",
                    "name": team_name
                }
            }
        }
        let cmd_json_string = JSON.stringify(keybase_team_topics_cmd_str)
        let command = ["keybase", "chat", "api", "-m", "'"+cmd_json_string+"'"].join(' ')
        team_topics = await JSON.parse(execSync(command).toString("utf8"))
        fs.writeFileSync(
            topic_file_name, 
            JSON.stringify(team_topics),
        (err) => {
            if (err) {
                throw err;
            }
            console.log(`team_memberships is saved to ${topic_file_name}.`);
        });
        return team_topics
    }
}



async function get_team_messages(){

}
async function main() {
    let keybase_user;
    let export_dir = "./exports"
    keybase_user = await get_keybase_user()
    console.log(`Currently logged in as ${keybase_user}`)
    // Create folder for user and their teams if it does not exist
    create_folder_if_not_exist(`${export_dir}/${keybase_user}`)
    create_folder_if_not_exist(`${export_dir}/${keybase_user}/teams`)
    // // Currently method_list is not used for anything
    // let method_list = get_method_list()
    // fs.writeFileSync(`${export_dir}/${keybase_user}/method_list.json`, JSON.stringify(method_list), (err) => {
    //     if (err) {
    //         throw err;
    //     }
    //     console.log(`team_memberships is saved to ${tmp_file_output}.`);
    // });
    // Export / Import list of teams user is on
    let team_memberships = await export_team_memberships(`${export_dir}/${keybase_user}/team_memberships.json`)
    console.log(`${team_memberships.length} teams were imported`)
    // export_teams_topics_metadata(export_dir, keybase_user, team_memberships)
    // Create a folder for every team, export the topics, plus export the messages
    for(var i = 0; i < team_memberships.length; i++){
        await get_team_topics(export_dir, keybase_user, team_memberships[i].Team)
    }

    // Export all topics for a single team
    let export_team_name = "dentropydaemon";
    let team_topics = await get_team_topics(export_dir, keybase_user, export_team_name)
    console.log(team_topics)
    for(var i = 0; i < team_topics.result.conversations.length; i++){
        let tmp_topic_messages = await get_keybase_topic(
            team_topics.result.conversations[i].channel.name,
            team_topics.result.conversations[i].channel.members_type,
            team_topics.result.conversations[i].channel.topic_name
        )
        fs.writeFileSync(`${export_dir}/${keybase_user}/teams/${export_team_name}/${team_topics.result.conversations[i].channel.topic_name}.json`, JSON.stringify(tmp_topic_messages), (err) => {
            if (err) {
                throw err;
            }
            console.log(`export of topic ${team_topics.result.conversations[i].channel.topic_name} for team ${export_team_name} is saved in ${tmp_file_output}.`);
        });
    }
    // Parse URL's
    // Parse Domain Name's
    // Connect Reactions

    process.exit(1)
}
main()