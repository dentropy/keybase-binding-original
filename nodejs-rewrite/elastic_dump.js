import { Client } from '@elastic/elasticsearch'
import fg from 'fast-glob'
import fs from 'fs'
const client = new Client({ 
    node: 'http://localhost:9200',
    auth: {
        username: 'elastic',
        password: 'rgIcWCIg2IMNmnoRIJMudHEXVVFyPk5'
    }
})

async function main(){
    let files_to_index = await fg.sync(["**/dentropy/teams/dentropydaemon/*.json", '!**/node_modules', '!**/dentropy/teams/dentropydaemon/topics.json'])
    files_to_index.forEach((topic_messages) => {
        let file_content = fs.readFileSync(topic_messages, 'utf8')
        let dataset = JSON.parse(file_content)
        console.log(dataset)
        dataset.forEach((tmp_message) => {
            client.index({
                index: 'test294',
                body: tmp_message
            })
        })
    })
}
main()