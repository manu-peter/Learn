const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const DB_API_URL = process.env.DB_API_URL || 'http://db-api:8000';

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'backend-api', version: 'v3-canary' });
});

app.get('/api/info', (req, res) => {
  res.json({ version: 'v3-canary', message: '🚀 You hit the CANARY version! This is the new v3!' });
});

app.get('/api/tasks', async (req, res) => {
  try {
    const response = await axios.get(`${DB_API_URL}/tasks`);
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/tasks', async (req, res) => {
  try {
    const { title, description } = req.body;
    const response = await axios.post(`${DB_API_URL}/tasks`, { title, description });
    res.status(201).json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => console.log('Backend running on 5000'));
// test trivy fix
