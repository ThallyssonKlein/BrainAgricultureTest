import React, { createContext, useState } from 'react';
import { ICrop } from '../components/IFarmer';

export const CropModalContext = createContext<
    {
        isEdit: boolean;
        setISEdit: React.Dispatch<React.SetStateAction<boolean>>;
        modalIsOpen: boolean;
        setModalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
        selectedCrop: ICrop | null;
        setSelectedCrop: React.Dispatch<React.SetStateAction<ICrop | null>>;
    }
>({
    isEdit: false,
    setISEdit: () => {},
    modalIsOpen: false,
    setModalIsOpen: () => {},
    selectedCrop: null,
    setSelectedCrop: () => {}
});

interface CropModalProviderProps {
  children: React.ReactNode;
}

export const CropModalContextProvider = ({ children }: CropModalProviderProps) => {
    const [isEdit, setISEdit] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [selectedCrop, setSelectedCrop] = useState<ICrop | null>(null);
  
    return (
        <CropModalContext.Provider value={{
            isEdit,
            setISEdit,
            modalIsOpen,
            setModalIsOpen,
            selectedCrop,
            setSelectedCrop
        }}>
            {children}
        </CropModalContext.Provider>
    );
};
