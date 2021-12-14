import axios from "axios";
import { stringify } from "postcss";

const Twitter = require('twitter-v2');

const telegramBot = async (req, res) => {
    if (req.query.token != process.env.TELEGRAM_WEBHOOK_TOKEN) {
        res.statuscode = 401
        res.json({ 'error': 'unathorized', 'message': 'invalid token' });
        return
    }

    const message = req.body.message.text;
    const user = req.body.message.from;

    if (message === "/f") {
        const client = new Twitter({
            bearer_token: process.env.TWITTER_BEARER_TOKEN
        });

        const user = await client.get('users/1457120903695724545',{'user.fields': ['public_metrics']});
        
        const telegramToken = process.env.TELEGRAM_TOKEN
        const telegramParams = {
            'parse_mode': 'HTML',
            'chat_id': parseInt(process.env.TELEGRAM_CHAT_ID),
            'text': 'Followers: ' + JSON.stringify(user.data.public_metrics.followers_count)
        }
        
        const res = await axios.get(`https://api.telegram.org/bot${telegramToken}/sendMessage`, { params: telegramParams })

        if (res.status != 200) {
            console.log(res);
        }
    }

    if (message === '/t') {
        const client = new Twitter({
            bearer_token: process.env.TWITTER_BEARER_TOKEN
        });

        const user = await client.get('users/1457120903695724545',{'user.fields': ['public_metrics']});
        
        const telegramToken = process.env.TELEGRAM_TOKEN
        const telegramParams = {
            'parse_mode': 'HTML',
            'chat_id': parseInt(process.env.TELEGRAM_CHAT_ID),
            'text': 'Tweets: ' + JSON.stringify(user.data.public_metrics.tweet_count)
        }
        
        const res = await axios.get(`https://api.telegram.org/bot${telegramToken}/sendMessage`, { params: telegramParams })

        if (res.status != 200) {
            console.log(res);
        }
    }

    if (message === "/tf" || message === "/ft") {
        const client = new Twitter({
            bearer_token: process.env.TWITTER_BEARER_TOKEN
        });

        const user = await client.get('users/1457120903695724545',{'user.fields': ['public_metrics']});
        
        const telegramToken = process.env.TELEGRAM_TOKEN
        const telegramParams = {
            'parse_mode': 'HTML',
            'chat_id': parseInt(process.env.TELEGRAM_CHAT_ID),
            'text': 'Tweets: ' + JSON.stringify(user.data.public_metrics.tweet_count) + '\nFollowers: ' + JSON.stringify(user.data.public_metrics.followers_count)
        }
        
        const res = await axios.get(`https://api.telegram.org/bot${telegramToken}/sendMessage`, { params: telegramParams })

        if (res.status != 200) {
            console.log(res);
        }
    }

    if (message === "/help") {
        const telegramToken = process.env.TELEGRAM_TOKEN
        const telegramParams = {
            'parse_mode': 'HTML',
            'chat_id': parseInt(process.env.TELEGRAM_CHAT_ID),
            'text': 'Supported commands\nt - Number of Tweets\nf - Number of Followers\nft, tf - Number of Tweets & Followers'
        }
        
        const res = await axios.get(`https://api.telegram.org/bot${telegramToken}/sendMessage`, { params: telegramParams })

        if (res.status != 200) {
            console.log(res);
        }
    }

    if (message === "/fu") {
        const telegramToken = process.env.TELEGRAM_TOKEN
        const telegramParams = {
            'parse_mode': 'HTML',
            'chat_id': parseInt(process.env.TELEGRAM_CHAT_ID),
            'text': '\uD83D\uDD95 Fuck you ' + user.first_name + ' \uD83D\uDD95'
        }
        
        const res = await axios.get(`https://api.telegram.org/bot${telegramToken}/sendMessage`, { params: telegramParams })

        if (res.status != 200) {
            console.log(res);
        }
    }


    res.json({ "message":"done" })
}

export default telegramBot    