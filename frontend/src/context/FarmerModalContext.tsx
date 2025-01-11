import React, { createContext, useState } from 'react';

export const FarmerModalContext = createContext<
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
    setModalIsOpen: () => {}
});

interface FarmerProviderProps {
  children: React.ReactNode;
}

export const FarmerModalContextProvider = ({ children }: FarmerProviderProps) => {
    const [isEdit, setISEdit] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(false);
  
    return (
        <FarmerModalContext.Provider value={{
            isEdit,
            setISEdit,
            modalIsOpen,
            setModalIsOpen
        }}>
            {children}
        </FarmerModalContext.Provider>
    );
};
