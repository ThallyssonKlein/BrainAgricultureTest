import React from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsProvider } from "../../context/OptionsContext";
import Chart from "../../components/chart/Chart";

export default function Dashboard() {
    const handleClick = () => {
        // Define the action to be triggered on button click
        console.log("Create button clicked");
    };

    return (
        <OptionsProvider>
            <div>
                <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                        <PaginatedSelect />
                    <button onClick={handleClick}>
                            Create
                    </button>
                </div>
                <Chart />
            </div>
        </OptionsProvider>
    )
}