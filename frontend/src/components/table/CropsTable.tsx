import React, { JSX, useContext, useState } from "react";
import { ICrop } from "../IFarmer";
import { CropModalContext } from "../../context/CropModalContext";
import CropModal from "../CropModal";
import API from "../../API";
import { OptionsContext } from "../../context/OptionsContext";
import { TablesContext } from "../../context/TablesContext";

export default function CropsTable(): JSX.Element {
    const { setModalIsOpen, setISEdit } = useContext(CropModalContext);
    const [selectedCrop, setSelectedCrop] = useState<ICrop | null>(null);
    const { setRefreshCharts } = useContext(OptionsContext);
    const { crops, farms, setCrops, selectedFarmId, setFarms } = useContext(TablesContext);

    const handleDeleteCrop = async (id: number) => {
      const userResponse = window.confirm("Do you want to proceed?");
      if (userResponse) {
        const response = await API.delete(`/api/v1/crop/${id}`);

        if (response.status === 200){
            const selectedFarm = farms.find(farm => farm.id === selectedFarmId);
            if (selectedFarm) {
                setFarms(prevFarms => prevFarms.map(farm => 
                    farm.id === selectedFarmId 
                    ? { ...farm, crops: farm.crops?.filter(crop => crop.id !== id) || [] } 
                    : farm
                ));
            } else {
                setCrops((previousCrops) => previousCrops.filter(crop => crop.id !== id));
            }
            setRefreshCharts(previos => previos + 1);
        } else {
          alert("Error deleting!");
        }
      }
    }

    return (
        <div>
          <CropModal selectedCrop={selectedCrop} />
          <table border={1} style={{ width: '100%', marginBottom: '20px', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ minWidth: '50px', width: '1%' }}>Id</th>
                <th style={{ minWidth: '100px', width: '10%' }}>Data</th>
                <th style={{ width: 'auto' }}>Nome da Cultura</th>
                <th style={{ minWidth: '80px', width: '1%' }}>Editar</th>
                <th style={{ minWidth: '80px', width: '1%' }}>Excluir</th>
              </tr>
            </thead>
            <tbody>
              {selectedFarmId ? farms.find(farm => farm.id === selectedFarmId)?.crops?.map((crop) => (
                <tr
                  key={crop.id}
                  style={{ cursor: 'pointer', background: 'white' }}
                >
                  <td>{crop.id}</td>
                  <td>{crop.date}</td>
                  <td>{crop.culture?.name}</td>
                  <td>
                    <button
                      onClick={() => {
                        setISEdit(true);
                        setSelectedCrop(crop);
                        setModalIsOpen(true);
                      }}
                    >Edit</button>
                  </td>
                  <td>
                    <button onClick={(_event) => handleDeleteCrop(crop.id)}>Delete</button>
                  </td>
                </tr>
              )) : crops?.map((crop) => (
                <tr
                  key={crop.id}
                  style={{ cursor: 'pointer', background: 'white' }}
                >
                  <td>{crop.id}</td>
                  <td>{crop.date}</td>
                  <td>{crop.culture_name}</td>
                  <td>
                    <button
                      onClick={() => {
                        setISEdit(true);
                        setSelectedCrop(null);
                        setSelectedCrop(crop);
                        setModalIsOpen(true);
                      }}
                    >Edit</button>
                  </td>
                  <td>
                    <button onClick={(_event) => handleDeleteCrop(crop.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
              <button 
                style={{flex: 1}}
                onClick={() => setModalIsOpen(true)}
              >Create Crop</button>
          </div>
        </div>
    )
}