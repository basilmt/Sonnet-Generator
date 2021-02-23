# Sonnet Generator

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened",
    "stats" : "complete",
    "url-endpoint" : "/lines" --not mandatory
}
```

### stuffs1

**Definition**

`GET /`

**Response**

- `200 OK` on success

```json
{ 
    "data" : "Hello Person",
    "message" : "to get to documentation - /docs" ,
    "stats" : "complete"
}
```

### stuffs2

**Definition**

`GET /greet`

**Response**

- `200 OK` on success

eg : '/greet'

```json
{ 
    "data" : "Hello Random Person",
    "message" : "to get to documentation - /docs" ,
    "stats" : "complete"
}
```

### stuffs3

**Definition**

`GET /greet/<name>`

**Response**

- `200 OK` on success

eg : '/greet/boyy'

```json
{ 
    "data" : "Hello boyy",
    "message" : "to get to documentation - /docs" ,
    "stats" : "complete"
}
```

### Make a random line

**Definition**

`GET /line`

**Response**

- `200 ok` on success

eg : '/line'

```json
{
    "data":"our time , with heaven and blazing stars doth atlas stand",
    "message":"One line completed",
    "stats":"complete"
}
```

## Line with a starting word

`GET /line/<start>`

**Response**

- `200 OK` on success
- `204 No Content` on failure

eg : '/line/love'

```json
{
    "data":"love was the flame that doth my rest defeat",
    "message":"One line with starting love",
    "stats":"complete"
}
```

### A 10 lined sonnet

**Definition**

`GET /lines`

**Response**

- `200 ok` on success

eg : '/lines'

```json
{
    "data":["and yse , which is death to hide","in cooling trees , a voice amid the quiet intense","and cling around about us as a gently widening stream","like you , who hast gone out there","let dost thought of ioy , the blossome of the morne","be it known , that the world be helped","night reels with tumult ; and , impetuous , vents","warblest at eve , when all those days ay o'er","a gulfy sea , the day had now unfurled","sleeps the keen magic of each day \u2019 s demand"],
    "message":"10 lines completed",
    "stats":"complete"
}
```

### A sonnet with our choice of lines

**Usage**

We can only get 8 lines at a time  
so use the next def wisely to get long sonnets 

**Definition**

`GET /lines/<number_of_lines>`

**Response**

- `200 ok` on success

eg : '/lines/5'

```json
{
    "lines":["\u201c treat foreigners to that , \u201d the solitary shadow quick","sense of touch , or prompt one happy line","and through the air the angels swam","led by love , thy truth , thy constancy","although i swear it to my soul than its soul life"],
    "message":"5 lines completed",
    "stats":"complete"
}
```

if line number is long (>8)  
you'll get a url endpoint  
use that to make remaining lines  
until you get stats as complete  

eg : '/lines/25'

```json
{
    "lines":["who doubts of this , should i twenty kisses take away","i say , go , expose thy charms","alas ! in vain the labouring engines pour","out their oil , when the day of reckoning had come","out of it , my soul , and fear his nod","the soil is this , that you alone , aught you","will , there is hast dram of blood","of elders like the blood of doges in your cheek"],
    "message":"8 lines made, 17 to go",
    "stats":"incomplete",
    "url-endpoint":"/lines/25/8/cheek"
}
```

### Really long sonnet

**Usage**

We can only get 8 lines at a time  
so use this wisely to get long sonnets  

**Definition**

`GET /lines/<number_of_lines>/<number_of_lines_rendered>/<memory>`

**Response**

- `200 ok` on success  

eg : '/lines/25/8/cheek'

```json
{
    "data":["and languish in the eyes of the true and just","so the glutton whom the world could not hold argument","revive , transfigured , but in her last","shall bow down to heads untitled , and the cross absent","yet , lord , thy slaughtered saints , whose bones","liked the attic , let them consent to go","arm your sons ! drums beat and trumpets blow","burn , and make hast further know"],
    "message":"16 lines made, 9 to go",
    "stats":"incomplete",
    "url-endpoint":"/lines/25/16/know"
}
```

