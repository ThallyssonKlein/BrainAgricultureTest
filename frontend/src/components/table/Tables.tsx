import React, { useState, useContext, useEffect } from 'react';
import { TablesContext } from '../../context/TablesContext';
import "./table.css"
import CropsTable from './CropsTable';
import { IFarm } from '../IFarmer';

const FarmTable: React.FC = () => {
  const [selectedFarmId, setSelectedFarmId] = useState<number | null>(null);
  const { farms, crops, setSelectedFarm, selectedFarm } = useContext(TablesContext);

  const handleFarmClick = (farmId: number) => {
    setSelectedFarmId(farmId === selectedFarmId ? null : farmId);
    setSelectedFarm(farms.find((farm) => farm.id === farmId) || null);
  };

  return (
    <div className="farms-table-container">
      {farms && farms.length > 0 && (!crops || crops.length === 0)&& 
        <div>
        {/* Tabela de Fazendas */}
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
              </tr>
            ))}
          </tbody>
        </table>

        <h3>Crops</h3>
        {selectedFarm && (
          <CropsTable
            selectedFarm={selectedFarm}
            setSelectedFarm={setSelectedFarm}
          />
        )}
      </div>
      }
      {crops && crops.length > 0 && (!farms || farms.length === 0) &&
        <div>
          <h3>Crops</h3>
          {crops && (
            <CropsTable
              crops={crops}
            />
          )}
        </div>
      }
    </div>
  );
};

export default FarmTable;
