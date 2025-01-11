import React from "react";
import PieChart from "./PieChart";
import "./charts.css"
import { IData } from "./IData";

export default function withFilledPieCharts(data: IData) {
  const labelsState = []
  const dataState = []

  for (const state of data.farm_counts_grouped_by_state) {
    labelsState.push(state.state);
    dataState.push(state.farm_count);
  }

  const labelsCulture = []
  const dataCulture = []

  for (const culture of data.farms_count_grouped_by_culture) {
    labelsCulture.push(culture.culture);
    dataCulture.push(culture.farm_count);
  }

  const landUseLabels = ["Arable Area", "Vegetation Area"];
  const landUseData = [
    data.average_land_use.average_arable_area,
    data.average_land_use.average_vegetation_area,
  ];

  return (
    <div className="pie-charts-container">
      <div className="pie-chart">
        <PieChart labels={labelsState} data={dataState} />
      </div>
      <div className="pie-chart">
        <PieChart labels={labelsCulture} data={dataCulture} />
      </div>
      <div className="pie-chart">
        <PieChart labels={landUseLabels} data={landUseData} />
      </div>
    </div>
  );
}