import React from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsProvider } from "../../context/OptionsContext";
import Charts from "../../components/charts/Charts";
import { TablesContextProvider } from "../../context/TablesContext";
import Tables from "../../components/table/Tables";

export default function Dashboard() {
    const handleClick = () => {
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
                <TablesContextProvider>
                    <Charts />
                    <Tables />
                </TablesContextProvider>
            </div>
        </OptionsProvider>
    )
}