import React from "react";

interface ICulturesTableProps {
    selectedCrop: {
        culture: {
            id: number;
            name: string;
        }
    }
}

export default function CulturesTable({ selectedCrop }: ICulturesTableProps): JSX.Element {
    return (
        <table border={1} style={{ width: '100%' }}>
            <thead>
              <tr>
                <th>Id</th>
                <th>Nome da Cultura</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{selectedCrop.culture?.id}</td>
                <td>{selectedCrop.culture?.name}</td>
              </tr>
            </tbody>
          </table>
    )
}