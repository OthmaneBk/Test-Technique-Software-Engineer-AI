import { useEffect, useState } from "react";
import getdata from "./router";
import DataTable from "./components/DataTable";
import ChatAssistant from "./components/ChatAssistant";
import Header from "./components/Header";
import { TEXT } from "./constants/text";
import "./App.css";

export default function App() {
  const [data, setData] = useState([]);
  const [highlightTable, setHighlightTable] = useState(false);

  useEffect(() => {
    getdata()
      .then((result) => setData(result))
      .catch((err) => console.error(TEXT.app.loadError, err));
  }, []);

  async function refreshData(response) {
    if (response?.data) {
      setData(response.data);
    } else {
      const refreshed = await getdata();
      setData(refreshed);
    }
    setHighlightTable(true);
    setTimeout(() => setHighlightTable(false), 2000);
  }

  return (
    <div className="app">
      <Header onImported={refreshData} />

      <div className="app__body">
        <div className="app__main">
          <DataTable data={data} highlight={highlightTable} />
        </div>

        <ChatAssistant onShowAllData={refreshData} />
      </div>
    </div>
  );
}
