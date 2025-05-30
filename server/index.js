const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

//Middleware
app.use(cors());
app.use(express.json());

//Sample Route
app.get('/', (req, res) => {
    res.send('GP Booking Api is running!');
});

//Start Server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});