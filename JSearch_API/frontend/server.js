const express = require("express");
const fs = require("fs");
const path = require("path");
const request = require("request");

const app = express();
const PORT = 3000;

// Ensure the saved_searches directory exists
const savedSearchesDir = path.join(__dirname, "saved_searches");
if (!fs.existsSync(savedSearchesDir)) {
  fs.mkdirSync(savedSearchesDir);
}

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// Endpoint to get JSON data
app.get("/data", (req, res) => {
  fs.readFile("data.json", "utf8", (err, data) => {
    if (err) {
      res.status(500).send("Error reading data file");
      return;
    }
    res.json(JSON.parse(data));
  });
});

// Endpoint to handle search requests
app.get("/search", (req, res) => {
  const query = req.query.query || "software intern jobs in canada";
  const page = req.query.page || "1";
  const num_pages = req.query.num_pages || "1";
  const country = req.query.country || "ca";
  const date_posted = req.query.date_posted || "week";

  /**
   * Options for the HTTP request to the jsearch API.
   * 
   * @property {string} method - The HTTP method to use for the request.
   * @property {string} url - The URL of the jsearch API endpoint.
   * @property {Object} qs - The query string parameters for the request.
   * @property {string} qs.query - The search query.
   * @property {number} qs.page - The page number to retrieve.
   * @property {number} qs.num_pages - The number of pages to retrieve.
   * @property {string} qs.country - The country to filter the search results.
   * @property {string} qs.date_posted - The date the job was posted.
   * @property {Object} headers - The headers for the request.
   * @property {string} headers["x-rapidapi-key"] - The API key for authentication.
   * @property {string} headers["x-rapidapi-host"] - The host of the jsearch API.
   */
  const options = {
    method: "GET",
    url: "https://jsearch.p.rapidapi.com/search",
    qs: {
      query,
      page,
      num_pages,
      country,
      date_posted,
    },
    headers: {
      "x-rapidapi-key": "apikeyhere",
      "x-rapidapi-host": "jsearch.p.rapidapi.com",
    },
  };

  request(options, (error, response, body) => {
    if (error) {
      res.status(500).send("Error fetching data from API");
      return;
    }

    const responseData = JSON.parse(body);

    // Prettify JSON
    const prettyJson = JSON.stringify(responseData, null, 4);

    // Save to data.json
    fs.writeFile("data.json", prettyJson, (err) => {
      if (err) {
        res.status(500).send("Error saving data to file");
        return;
      }
      res.json(responseData);
    });
  });
});

// Endpoint to save search results with a timestamp
app.post("/save", (req, res) => {
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const filePath = path.join(savedSearchesDir, `${timestamp}.json`);

  fs.readFile("data.json", "utf8", (err, data) => {
    if (err) {
      res.status(500).send("Error reading data file");
      return;
    }

    fs.writeFile(filePath, data, (err) => {
      if (err) {
        res.status(500).send("Error saving search data");
        return;
      }
      res.send({ message: "Search data saved successfully", timestamp });
    });
  });
});

// Endpoint to list saved searches
app.get("/saved-searches", (req, res) => {
  fs.readdir(savedSearchesDir, (err, files) => {
    if (err) {
      res.status(500).send("Error reading saved searches directory");
      return;
    }

    const searches = files.map((file) => ({
      timestamp: file.replace(".json", ""),
      file,
    }));

    res.json(searches);
  });
});

// Endpoint to load a specific saved search
app.get("/load-search", (req, res) => {
  const timestamp = req.query.timestamp;
  const filePath = path.join(savedSearchesDir, `${timestamp}.json`);

  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      res.status(500).send("Error reading saved search file");
      return;
    }

    res.json(JSON.parse(data));
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});