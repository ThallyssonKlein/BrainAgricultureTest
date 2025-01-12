import React, { JSX, useContext } from "react";
import { ICrop, IFarm } from "../IFarmer";
import { CropModalContext } from "../../context/CropModalContext";
import CreateCropModal from "../CreateCropModal";

interface ICropsTableProps {
    selectedFarm?: IFarm;
    setSelectedFarm?: React.Dispatch<React.SetStateAction<IFarm | null>>;
    crops?: ICrop[]
}

export default function CropsTable({ selectedFarm, crops, setSelectedFarm }: ICropsTableProps): JSX.Element {
    const { setModalIsOpen } = useContext(CropModalContext);

    return (
        <div>
          <CreateCropModal selectedFarm={selectedFarm} setSelectedFarm={setSelectedFarm} />
          <table border={1} style={{ width: '100%', marginBottom: '20px' }}>
            <thead>
              <tr>
                <th>Id</th>
                <th>Data</th>
                <th>Nome da Cultura</th>
              </tr>
            </thead>
            <tbody>
              {selectedFarm ? selectedFarm.crops?.map((crop) => (
                <tr
                  key={crop.id}
                  style={{ cursor: 'pointer', background: 'white' }}
                >
                  <td>{crop.id}</td>
                  <td>{crop.date}</td>
                  <td>{crop.culture?.name}</td>
                </tr>
              )) : crops?.map((crop) => (
                <tr
                  key={crop.id}
                  style={{ cursor: 'pointer', background: 'white' }}
                >
                  <td>{crop.id}</td>
                  <td>{crop.date}</td>
                  <td>{crop.culture_name}</td>
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