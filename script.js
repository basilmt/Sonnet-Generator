var arr = []
var STATUS_INCOMPLETE = "incomplete"
var STATUS_COMPLETE = "complete"
var STATUS_FAILED = "failed"

ur = '/lines/14'
requester(ur)

function requester(url) {
    var request = new XMLHttpRequest()
    const baseurl = 'https://sonnet-gen.herokuapp.com'
    request.open('GET', baseurl + url, true)
    request.onload = function () {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response)
        if (request.status >= 200 && request.status < 400) {
            console.log(data)
            data.data.forEach((line) => {
                console.log(line)
                arr.push(line)

                const container = document.getElementById('container')
                const p = document.createElement('p')
                p.innerText = line
                container.appendChild(p)

            })
            if (data.stats === STATUS_INCOMPLETE) {

                requester(data["url-endpoint"])
            }
            else if (data.stats === STATUS_COMPLETE) {
                // populate()
            }
            
            console.log(arr);
        }
        else {
            alert("baddd")
        }
    }

    request.send()
}
function populate() {
    const container = document.getElementById('container')
    arr.forEach((line) => {
        const p = document.createElement('p')
        p.innerText = line
        container.appendChild(p)
    })

}

