import "../css/DataTable.css";
import { TEXT } from "../constants/text";

export default function DataTable({ data, highlight }) {
  return (
    <section className={`data-table ${highlight ? "data-table--highlight" : ""}`}>
      <div className="data-table__heading">
        <h2 className="data-table__title">{TEXT.dataTable.title}</h2>
        <span className="data-table__count">{data.length} {TEXT.dataTable.countSuffix}</span>
      </div>

      <div className="data-table__scroll">
        {data.length === 0 ? (
          <div className="data-table__empty">{TEXT.dataTable.empty}</div>
        ) : (
          <table>
            <thead>
              <tr>
                {Object.keys(data[0]).map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row.id}>
                  {Object.values(row).map((val, i) => (
                    <td key={i}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
