import React, { createContext, useState } from 'react';

export const CropModalContext = createContext<
    {
        isEdit: boolean;
        setISEdit: React.Dispatch<React.SetStateAction<boolean>>;
        modalIsOpen: boolean;
        setModalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    }
>({
    isEdit: false,
    setISEdit: () => {},
    modalIsOpen: false,
    setModalIsOpen: () => {},
});

interface CropModalProviderProps {
  children: React.ReactNode;
}

export const CropModalContextProvider = ({ children }: CropModalProviderProps) => {
    const [isEdit, setISEdit] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(false);
  
    return (
        <CropModalContext.Provider value={{
            isEdit,
            setISEdit,
            modalIsOpen,
            setModalIsOpen,
        }}>
            {children}
        </CropModalContext.Provider>
    );
};
