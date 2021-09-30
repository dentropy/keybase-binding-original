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
async function get_team_topics(tmp_team_name){
    let keybase_team_topics_cmd_str = {
        "method": "listconvsonname",
        "params": {
            "options": {
                "topic_type": "CHAT",
                "members_type": "team",
                "name": tmp_team_name
            }
        }
    }
    let cmd_json_string = JSON.stringify(keybase_team_topics_cmd_str)
    let command = ["keybase", "chat", "api", "-m", "'"+cmd_json_string+"'"].join(' ')
    let response_object = await JSON.parse(execSync(command).toString("utf8"))
    return response_object
}

async function get_keybase_topic(tmp_channel_name, tmp_members_type, tmp_topic_name, tmp_pagiation_next){
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
                    "num": 128
                }
            }
        }
    }
    if (tmp_pagiation_next != undefined) {
        keybase_topic_messages_cmd_str.params.options.pagination.next = tmp_pagiation_next
    }
    let cmd_json_string = JSON.stringify(keybase_topic_messages_cmd_str)
    let command = ["keybase", "chat", "api", "-m", "'"+cmd_json_string+"'"].join(' ')
    console.log(command)
    let response_object = await JSON.parse(execSync(command).toString("utf8"))
    return response_object
}

async function export_keybase_topic(tmp_file_output, tmp_channel_name, tmp_members_type, tmp_topic_name){
    let messages = await get_keybase_topic(tmp_channel_name, tmp_members_type, tmp_topic_name)
    while (!messages.result.pagination.last){
        messages = await get_keybase_topic(tmp_channel_name, tmp_members_type, tmp_topic_name, messages.result.pagination.last.next)
    }
    fs.writeFileSync(tmp_file_output, JSON.stringify(messages), (err) => {
        if (err) {
            throw err;
        }
        console.log(`Channel ${tmp_channel_name} topic ${tmp_topic_name} messages are saved to ${tmp_file_output}.`);
    });
}

async function get_method_list(tmp_file_output){
    let cmd_json_string = JSON.stringify({"method": "list"})
    let command = ["keybase", "chat", "api", "-m", "'"+cmd_json_string+"'"].join(' ')
    let response_object = JSON.parse(execSync(command).toString("utf8"))
    fs.writeFileSync(tmp_file_output, JSON.stringify(response_object), (err) => {
        if (err) {
            throw err;
        }
        console.log(`team_memberships is saved to ${tmp_file_output}.`);
    });
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

async function main() {
    let keybase_user;
    let export_dir = "./exports"
    let team_memberships = [];
    let method_list;
    keybase_user = await get_keybase_user()
    console.log(`Currently logged in as ${keybase_user}`)
    // Create folder for user if it does not exist
    create_folder_if_not_exist(`${export_dir}/${keybase_user}`)
    create_folder_if_not_exist(`${export_dir}/${keybase_user}/teams`)
    // Export / Import list of teams user is on
    // let team_memberships_file = `./${export_dir}/${keybase_user}/team_memberships.json`
    // if (fs.existsSync(team_memberships_file)) {
    //     var input = await question('Use existing team_memberships export (y or n)? ')
    //     if (input.match(/^y(es)?$/i)) { 
    //         console.log("Using existing team memberships")
    //         team_memberships = await JSON.parse(fs.readFileSync(team_memberships_file, 'utf8'));
    //     }
    //     else {
    //         console.log("Creating a new export")
    //         team_memberships = await export_team_memberships(team_memberships_file)
    //     }
    // }
    // else {
    //     team_memberships = await export_team_memberships(team_memberships_file)
    // }
    // console.log(`${team_memberships.length} teams were imported`)
    // let method_list_file = `./${export_dir}/${keybase_user}/method_list.json`
    // if (fs.existsSync(method_list_file)) {
    //     var input = await question('Use existing method_list export (y or n)? ')
    //     if (input.match(/^y(es)?$/i)) { 
    //         console.log("Using existing team memberships")
    //         team_memberships = await JSON.parse(fs.readFileSync(method_list_file, 'utf8'));
    //     }
    //     else {
    //         console.log("Creating a new export")
    //         team_memberships = await get_method_list(method_list_file)
    //     }
    // }
    // else {
    //     team_memberships = await get_method_list(method_list_file)
    // }
    // get_keybase_topic(
    //     `./${export_dir}/${keybase_user}/method_list.json`
    // )
    // get_keybase_topic(tmp_file_output, tmp_channel_name, tmp_members_type, tmp_topic_name, tmp_pagiation_next)
    // await export_keybase_topic(
    //     `${export_dir}/${keybase_user}/teams/dentropydaemon.json`,
    //     "dentropydaemon",
    //     "team",
    //     "bot-testing"
    // )
    console.log(util.inspect(await get_team_topics("dentropydaemon"), {depth: null}));

    // Create a folder for every team
    // Export topic names for every team
    // Export messages for every team
    //   Add metadata to JSON such as, Num Reactions, Number of URL's, list of root domain for URL, URL's, Check Mentions

    process.exit(1)
    // team_memberships = await get_team_memberships(`./${export_dir}/${keybase_user}/team_memberships.json`)
    //console.log(team_memberships)
    // if (team_memberships.length == 0){
    //     console.log("Error, no teams in team_memberships file")
    //     process.exit(1)
    // }
    // console.log(team_memberships)
    // if (await check_for_user_folder()) {
    //     create_user_folder()
    // }
    //get_team_memberships()

}
main()