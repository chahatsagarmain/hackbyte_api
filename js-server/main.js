const express = require("express");
const axios = require('axios');

async function sendRawText(pdf_id, user_id , raw_text) {

    console.log(typeof raw_text)
    
    const data = {
        pdf_id: pdf_id,
        data: raw_text,
        user_id: user_id
    };

    const headers = {
        "Content-Type": "application/json",
        // Add any other headers that you need
    };

    try {
        const response = await axios.post('https://fb16-14-139-241-214.ngrok-free.app/upload/', data, { headers: headers });
        console.log(response.data);
    } catch (error) {
        console.error(`Error: ${error}`);
    }
}


async function qna(pdf_id, user_id , message) {
    
    const data = {
        pdf_id: pdf_id,
        query: message,
        user_id: user_id,
        toxic_check : true
    };

    const headers = {
        "Content-Type": "application/json",
        // Add any other headers that you need
    };

    try {
        const response = await axios.post('https://fb16-14-139-241-214.ngrok-free.app/qna/', data, { headers: headers });
        console.log(response.data);
        return response.data
    } catch (error) {
        console.error(`Error: ${error}`);
    }
}


const app = express();

app.use(express.json());


app.post("/" ,async (req , res) => {

    await sendRawText(req.body.pdf_id, req.body.user_id , req.body.text)
    return res.status(200).json({"messag" : "done"})
});

app.post("/qna" , async (req , res) => {
    console.log(req.body)
    const response = await qna(req.body.pdf_id, req.body.user_id , req.body.query)
    console.log(response)
    return res.status(200).json({"response" : response})
});

app.listen(7000, () => {
    console.log('Server is running on localhost:7000');
});

