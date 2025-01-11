import React, { useState } from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsContextProvider } from "../../context/OptionsContext";
import Charts from "../../components/charts/Charts";
import { TablesContextProvider } from "../../context/TablesContext";
import Tables from "../../components/table/Tables";
import CreateFarmerModal from "../../components/CreateFarmerModal";
import { FarmerContextProvider } from "../../context/FarmerContext";
import CreateButton from "../../components/CreateButton";
import EditButton from "../../components/EditButton";
import DeleteButton from "../../components/DeleteButton";

export default function Dashboard() {
        return (
        <OptionsContextProvider>
            <FarmerContextProvider>
                <CreateFarmerModal />
                <div>
                    <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                            <PaginatedSelect />
                            <CreateButton />
                            <EditButton />
                            <DeleteButton />
                    </div>
                    <TablesContextProvider>
                        <Charts />
                        <Tables />
                    </TablesContextProvider>
                </div>
            </FarmerContextProvider>
        </OptionsContextProvider>
    )
}