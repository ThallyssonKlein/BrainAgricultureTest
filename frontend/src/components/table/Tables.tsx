import React, { useContext } from 'react';
import { TablesContext } from '../../context/TablesContext';
import "./table.css"
import CropsTable from './CropsTable';
import { FarmModalContext } from '../../context/FarmModalContext';
import API from '../../API';
import { OptionsContext } from '../../context/OptionsContext';

const Tables: React.FC = () => {
  const { setFarms, farms, crops, setSelectedFarmId, selectedFarmId } = useContext(TablesContext);

  const { setModalIsOpen, setISEdit } = useContext(FarmModalContext);

  const { setRefreshCharts } = useContext(OptionsContext);

  const handleFarmClick = (farmId: number) => {
    const selectedFarm = farms.find((farm) => farm.id === farmId);
    setSelectedFarmId(selectedFarm ? selectedFarm.id : null);
  };

  const handleDeleteFarm = async (id: number) => {
    const userResponse = window.confirm("Do you want to proceed?");
    if (userResponse) {
        const response = await API.delete(`/api/v1/farm/${id}`);

        if (response.status === 200){
            setSelectedFarmId(null);
            setFarms(farms.filter((farm) => farm.id !== id));
            setRefreshCharts(previos => previos + 1);
        } else {
            alert("Error deleting!");
        }
     }
  }

  return (
    <div className="farms-table-container">
      {farms && farms.length > 0 && (!crops || crops.length === 0) && 
        <div>
        <h2>Click on the farm to see the crops</h2>
        <h3>Farms</h3>
        <table border={1} style={{ width: '100%', marginBottom: '20px' }}>
          <thead>
            <tr>
              <th>Id</th>
              <th>Nome</th>
              <th>Área Total</th>
              <th>Área Vegetação</th>
              <th>Área Arável</th>
              <th>Estado</th>
              <th>Cidade</th>
              <th>Editar</th>
              <th>Excluir</th>
            </tr>
          </thead>
          <tbody>
            {farms.map((farm) => (
              <tr
                key={farm.id}
                onClick={() => handleFarmClick(farm.id)}
                style={{ cursor: 'pointer', background: selectedFarmId === farm.id ? '#f0f0f0' : 'white' }}
              >
                <td>{farm.id}</td>
                <td>{farm.name}</td>
                <td>{farm.total_area}</td>
                <td>{farm.vegetation_area}</td>
                <td>{farm.arable_area}</td>
                <td>{farm.state}</td>
                <td>{farm.city}</td>
                <td>
                  <button
                    onClick={() => {
                      setISEdit(true);
                      setSelectedFarmId(null);
                      setSelectedFarmId(farm.id);
                      setModalIsOpen(true);
                    }}
                  >Edit</button>
                </td>
                <td>
                  <button onClick={(event) => handleDeleteFarm(farm.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {selectedFarmId && (
          <div>
            <h3>Crops</h3>
            <CropsTable />
          </div>
        )}
      </div>
      }
      {crops && crops.length > 0 && (!farms || farms.length === 0) &&
        <div>
          <h3>Crops</h3>
          {crops && (
            <CropsTable />
          )}
        </div>
      }
    </div>
  );
};

export default Tables;
