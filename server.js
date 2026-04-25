const express = require('express');
const path = require('path');
const app = express();

// Ordner mit deinen HTML-Dateien/Bildern
const templatesDir = path.join(__dirname, 'templates');
app.use(express.static(templatesDir));

app.get('/', (req, res) => {
  res.sendFile(path.join(templatesDir, 'index.html'));
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Static HTML auf http://localhost:${PORT}`));