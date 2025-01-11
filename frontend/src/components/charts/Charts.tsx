import React, { JSX, useContext, useEffect } from "react";
import { OptionsContext } from "../../context/OptionsContext";
import WithFilledPieCharts from "./WithFilledPieCharts";
import API from "../../API";
import { IData } from "./IData";

export default function Charts() {
    const { selectedOption } = useContext(OptionsContext);
    const [PieChartsComponent, setPieChartsComponent] = React.useState<JSX.Element | null>(null);
    const [data, setData] = React.useState<IData | null>(null);

    useEffect(() => {
        if (selectedOption) {
            API.get(`/api/v1/dashboard/${selectedOption}`).then((response) => {
                console.log(response.data)
                setData(response.data as IData);
            });
        }
    }, [selectedOption]);

    useEffect(() => {
        if (data) {
            setPieChartsComponent(<WithFilledPieCharts data={data} />);
        }
    }, [data]);

    return (
        <div>
            {data ? 
                <div>
                    <div className="counts-container">
                        <h1 className="count">Total Farms: {data ? data.farm_count : null}</h1>
                        <h1 className="count">Total Hectares: {data ? data.total_hectares : null}</h1>
                    </div>
                    {
                        data.farm_counts_grouped_by_state && data.farm_counts_grouped_by_state.length > 0 
                        && data.farms_count_grouped_by_culture && data.farms_count_grouped_by_culture.length > 0
                        && data.average_land_use 
                        && data.average_land_use.average_arable_area && data.average_land_use.average_arable_area > 0 
                        && data.average_land_use.average_vegetation_area && data.average_land_use.average_vegetation_area > 0 &&

                        <div className="charts-container">
                            <h1>Charts</h1>
                            <h2>Click on the slices of the charts to see the details</h2>
                            {selectedOption && PieChartsComponent ? PieChartsComponent : null }
                        </div>
                    }
                </div>
                :
                null
            }
        </div>
    )
}