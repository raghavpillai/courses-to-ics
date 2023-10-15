import React, { useEffect, useState } from "react";
import "@pages/popup/Popup.css";

const API_URL = "http://127.0.0.1:5000/api/v1/get_classes";

const Popup = () => {
  const [currentUrl, setCurrentUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [responseText, setResponseText] = useState(null);

  useEffect(() => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentTab = tabs[0];
      setCurrentUrl(currentTab.url);
    });
  }, []);

  const handleButtonClick = async () => {
    setLoading(true);
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      console.log(data);
      setResponseText(data.body.errors);
      const blob = new Blob([data.body.ics], { type: "text/calendar" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "schedule.ics");
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Get ICS from courses</h1>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <>
            <button
              disabled={!currentUrl || !currentUrl.includes("DACSPRD")}
              onClick={handleButtonClick}
            >
              Get ICS
            </button>
            {responseText && <p>{responseText}</p>}
          </>
        )}
      </header>
    </div>
  );
};

export default Popup;
