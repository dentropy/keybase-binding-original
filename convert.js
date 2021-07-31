// Requiring users file
const fs = require('fs');
const users = require("./exports/dentropydaemon-messages.json");
  
console.log(users);

let elastic_test = []

for (const key in users.topic_name) {
    console.log(`${key}: ${users.topic_name[key].result}`)
    for (let message_id in users.topic_name[key].result.messages) {
        let message = users.topic_name[key].result.messages[message_id].msg
        message.topic = key
        message.date = users.topic_name[key].result.messages[message_id].msg.sent_at_ms
        //let message = {key : users.topic_name[key].result}
        // console.log(message)
        message.category = key
        elastic_test.push(message)
        elastic_test.push(JSON.parse('{"index":{"_index":"companydatabase","_type":"employees"}}'));
    }


}


let final_string = ""

for (const key in elastic_test) {
    final_string += JSON.stringify(elastic_test[key]);
    final_string += "\n"
}

try {
    fs.writeFileSync('user.json', final_string);
    console.log("JSON data is saved.");
} catch (error) {
    console.error(error);
}