import React, { useContext, useEffect } from "react";
import { OptionsContext } from "../../context/OptionsContext";
import withFilledPieCharts from "./withFilledPieCharts";
import API from "../../API";

export default function Charts() {
    const { selectedOption } = useContext(OptionsContext);
    const [PieChartsComponent, setPieChartsComponent] = React.useState<JSX.Element | null>(null);
    const [data, setData] = React.useState<any | null>(null);

    useEffect(() => {
        if (selectedOption) {
            API.get(`/api/v1/dashboard/${selectedOption}`).then((response) => {
                console.log(response.data)
                setData(response.data);
            });
        }
    }, [selectedOption]);

    useEffect(() => {
        if (data) {
            setPieChartsComponent(withFilledPieCharts(data));
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
                    <div className="charts-container">
                        <h1>Charts</h1>
                        {selectedOption && PieChartsComponent ? PieChartsComponent : null }
                    </div>
                </div>
                :
                "Loading..."
            }
        </div>
    )
}