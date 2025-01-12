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
    const { setModalIsOpen, setISEdit, setSelectedCrop } = useContext(CropModalContext);

    return (
        <div>
          <CreateCropModal selectedFarm={selectedFarm} setSelectedFarm={setSelectedFarm} />
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
              {selectedFarm ? selectedFarm.crops?.map((crop) => (
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
                    <button>Delete</button>
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
                    <button>Delete</button>
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