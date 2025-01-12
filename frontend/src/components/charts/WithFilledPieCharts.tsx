import React, { JSX, useContext } from "react";
import PieChart from "./PieChart";
import "./charts.css"
import { IData } from "./IData";
import API from "../../API";
import { OptionsContext } from "../../context/OptionsContext";
import { TablesContext } from "../../context/TablesContext";
import { ICrop, IFarm } from "../IFarmer";

interface WithFilledPieChartsProps {
  data: IData;
}

export default function WithFilledPieCharts({ data }: WithFilledPieChartsProps): JSX.Element {
  const { selectedOption } = useContext(OptionsContext);
  const { setFarms, setCrops } = useContext(TablesContext);
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

  const landUseLabels = ["Área de Cultivo", "Área de Vegetação"];
  const landUseData = [
    data.average_land_use.average_arable_area,
    data.average_land_use.average_vegetation_area,
  ];

  const handleOnSlideClickGroupedByState = async (data: string) => {
    setCrops([])
    const response = await API.get("/api/v1/farm?state=" + data + "&farmer_id=" + selectedOption.id)

    if (response.status === 200) {
      setFarms(response.data as IFarm[]);
    }
  }

  const handleOnSlideClickGroupedByCulture = async (data: string) => {
    setFarms([])
    const response = await API.get("/api/v1/crop?culture_name=" + data + "&farmer_id=" + selectedOption.id)

    if (response.status === 200) {
      setCrops(response.data as ICrop[]);
    }
  }

  const handleOnSlideClickGroupedByArableAndVegetationArea = async (data: string) => {
    setCrops([])
    if (data === "Arable Area") {
      const response = await API.get("/api/v1/farm?order_by=arable_area_desc&farmer_id=" + selectedOption.id)

      if (response.status === 200) {
        setFarms(response.data as IFarm[]);
      }
    } else {
      const response = await API.get("/api/v1/farm?order_by=vegetation_area_desc&farmer_id=" + selectedOption.id)

      if (response.status === 200) {
        setFarms(response.data as IFarm[]);
      }
    }
  }

  return (
    <div className="pie-charts-container">
      {
        data.farm_counts_grouped_by_state && data.farm_counts_grouped_by_state.length > 0 ?
        <div className="pie-chart">
          <PieChart labels={labelsState} data={dataState} onSliceClick={handleOnSlideClickGroupedByState}/>
        </div>
        : null
      }
      {
        data.farms_count_grouped_by_culture && data.farms_count_grouped_by_culture.length > 0 ?
        <div className="pie-chart">
          <PieChart labels={labelsCulture} data={dataCulture} onSliceClick={handleOnSlideClickGroupedByCulture}/>
        </div>
      : null
      }
      {data.average_land_use && (data.average_land_use.average_arable_area && data.average_land_use.average_vegetation_area) ? 
        <div className="pie-chart">
          <PieChart labels={landUseLabels} data={landUseData} onSliceClick={handleOnSlideClickGroupedByArableAndVegetationArea}/>
        </div>
      : null
      }
    </div>
  );
}