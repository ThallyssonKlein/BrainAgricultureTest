import React, { useContext, useEffect } from 'react';
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
  
  useEffect(() => {
    console.log(farms)
  }, [farms])

  return (
    <div className="farms-table-container">
      {farms && farms.length > 0 && (!crops || crops.length === 0) && 
        <div>
        <h2>Clique em uma fazenda para ver suas safras</h2>
        <h3>Fazendas</h3>
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
                style={{ cursor: 'pointer', background: selectedFarmId === farm.id ? '#adacac' : 'white' }}
              >
                <td>{farm?.id || "N/A"}</td>
                <td>{farm?.name || "N/A"}</td>
                <td>{farm?.total_area || "N/A"}</td>
                <td>{farm?.vegetation_area || "N/A"}</td>
                <td>{farm?.arable_area || "N/A"}</td>
                <td>{farm?.state || "N/A"}</td>
                <td>{farm?.city || "N/A"}</td>
                <td>
                  <button
                    onClick={() => {
                      setISEdit(true);
                      setSelectedFarmId(null);
                      setSelectedFarmId(farm.id);
                      setModalIsOpen(true);
                    }}
                  >Editar</button>
                </td>
                <td>
                  <button onClick={(_event) => handleDeleteFarm(farm.id)}>Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {selectedFarmId && (
          <div>
            <h3>Safras</h3>
            <CropsTable />
          </div>
        )}
      </div>
      }
      {crops && crops.length > 0 && (!farms || farms.length === 0) &&
        <div>
          <h3>Safras</h3>
          {crops && (
            <CropsTable />
          )}
        </div>
      }
    </div>
  );
};

export default Tables;
