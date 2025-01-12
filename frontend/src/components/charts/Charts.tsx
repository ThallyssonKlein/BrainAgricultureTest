import React, { JSX, useContext, useEffect } from "react";
import { OptionsContext } from "../../context/OptionsContext";
import WithFilledPieCharts from "./WithFilledPieCharts";
import API from "../../API";
import { IData } from "./IData";

export default function Charts() {
    const { selectedOption, refreshCharts } = useContext(OptionsContext);
    const [PieChartsComponent, setPieChartsComponent] = React.useState<JSX.Element | null>(null);
    const [data, setData] = React.useState<IData | null>(null);

    useEffect(() => {
        if (selectedOption) {
            API.get(`/api/v1/dashboard/${selectedOption.id}`).then((response) => {
                setData(response.data as IData);
            });
        }
    }, [selectedOption, refreshCharts]);

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
                        <h1 className="count">Total de Fazendas: {data ? data.farm_count : null}</h1>
                        <h1 className="count">Total de Hectares: {data ? data.total_hectares : null}</h1>
                    </div>
                    {
                        (data.farm_counts_grouped_by_state && data.farm_counts_grouped_by_state.length > 0) 
                        || (data.farms_count_grouped_by_culture && data.farms_count_grouped_by_culture.length > 0) 
                        || (data.average_land_use && (data.average_land_use.average_arable_area && data.average_land_use.average_vegetation_area))
                        ?

                        <div className="charts-container">
                            <h1>Gráficos</h1>
                            <h2>Clique nas fatias do gráfico pra ver os detalhes</h2>
                            {selectedOption && PieChartsComponent ? PieChartsComponent : null }
                        </div>
                        : null
                    }
                </div>
                :
                null
            }
        </div>
    )
}