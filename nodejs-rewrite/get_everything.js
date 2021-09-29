import fs from 'fs';
import { exec, execSync, spawn } from 'child_process';
import readline from 'readline';
var rl = readline.createInterface(process.stdin, process.stdout);
import util from 'util' 
const question = util.promisify(rl.question).bind(rl);

//   info = {};

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

// Export each team chat to a file

// Export DM's to file

// Export Git Repos to file

// Create folder for user


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


async function main() {
    let keybase_user;
    let export_dir = "./exports/"
    let user_export_dir ;
    let team_memberships = [];
    keybase_user = await get_keybase_user()
    console.log(keybase_user)
    if (  fs.existsSync(`${export_dir}/${keybase_user}`)  ) {
        console.log("Folder Already Exists")
    }
    else {
        console.log()
        fs.mkdirSync(`${export_dir}/${keybase_user}`)
        console.log(`${export_dir}/${keybase_user} directory created successfully!`);
    }
    let team_memberships_file = `./${export_dir}/${keybase_user}/team_memberships.json`
    if (fs.existsSync(team_memberships_file)) {
        var input = await question('Use existing export (y or n)? ')
        if (input.match(/^y(es)?$/i)) { 
            console.log("Using existing team memberships")
            team_memberships = await JSON.parse(fs.readFileSync(team_memberships_file, 'utf8'));
        }
        else {
            console.log("Creating a new export")
            team_memberships = await export_team_memberships(team_memberships_file)
        }
    }
    else {
        team_memberships = await export_team_memberships(team_memberships_file)
    }
    console.log(`${team_memberships.length} teams were imported`)
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