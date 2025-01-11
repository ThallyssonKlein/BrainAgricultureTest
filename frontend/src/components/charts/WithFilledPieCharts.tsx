import React, { useContext } from "react";
import PieChart from "./PieChart";
import "./charts.css"
import { IData } from "./IData";
import API from "../../API";
import { OptionsContext } from "../../context/OptionsContext";
import { FarmsContext } from "../../context/FarmsContext";
import { IFarm } from "../paginated_select/IFarmer";

interface WithFilledPieChartsProps {
  data: IData;
}

export default function WithFilledPieCharts({ data }: WithFilledPieChartsProps): JSX.Element {
  const { selectedOption } = useContext(OptionsContext);
  const { setFarms } = useContext(FarmsContext);
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

  const handleOnSlideClickGroupedByState = async (data: string) => {
    const response = await API.get("/api/v1/farm?state=" + data + "&farmer_id=" + selectedOption)

    if (response.status === 200) {
      setFarms(response.data as IFarm[]);
    }
  }

  return (
    <div className="pie-charts-container">
      <div className="pie-chart">
        <PieChart labels={labelsState} data={dataState} onSliceClick={handleOnSlideClickGroupedByState}/>
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