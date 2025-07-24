const http = require('http');

const options = {
  hostname: 'localhost',
  port: 3000,
  path: '/',
  method: 'GET',
  timeout: 5000
};

const req = http.request(options, (res) => {
  console.log(`✅ React app is running on http://localhost:3000`);
  console.log(`Status: ${res.statusCode}`);
  process.exit(0);
});

req.on('error', (err) => {
  console.log(`❌ React app is not running on http://localhost:3000`);
  console.log(`Error: ${err.message}`);
  console.log(`\nTo start the app, run: npm start`);
  process.exit(1);
});

req.on('timeout', () => {
  console.log(`⏰ Timeout: React app is not responding`);
  process.exit(1);
});

req.end(); 