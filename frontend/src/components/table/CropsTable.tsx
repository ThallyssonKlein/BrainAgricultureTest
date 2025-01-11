import React, { JSX } from "react";
import { ICrop, IFarm } from "../IFarmer";

interface ICropsTableProps {
    selectedFarm?: IFarm;
    selectedCropId?: number | null;
    handleCropClick: (cropId: number) => void;
    crops?: ICrop[]
}

export default function CropsTable({ selectedFarm, selectedCropId, handleCropClick, crops }: ICropsTableProps): JSX.Element {
    return (
        <table border={1} style={{ width: '100%', marginBottom: '20px' }}>
            <thead>
              <tr>
                <th>Id</th>
                <th>Data</th>
                <th>Nome da Cultura</th>
              </tr>
            </thead>
            <tbody>
              {selectedFarm ? selectedFarm.crops.map((crop) => (
                <tr
                  key={crop.id}
                  onClick={() => handleCropClick(crop.id)}
                  style={{ cursor: 'pointer', background: selectedCropId === crop.id ? '#f0f0f0' : 'white' }}
                >
                  <td>{crop.id}</td>
                  <td>{crop.date}</td>
                  <td>{crop.culture?.name}</td>
                </tr>
              )) : crops?.map((crop) => (
                <tr
                  key={crop.id}
                  onClick={() => handleCropClick(crop.id)}
                  style={{ cursor: 'pointer', background: selectedCropId === crop.id ? '#f0f0f0' : 'white' }}
                >
                  <td>{crop.id}</td>
                  <td>{crop.date}</td>
                  <td>{crop.culture_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
    )
}