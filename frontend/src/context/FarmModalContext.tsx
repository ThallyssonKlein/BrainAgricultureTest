import React, { createContext, useState } from 'react';

export const FarmModalContext = createContext<
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

interface FarmProviderProps {
  children: React.ReactNode;
}

export const FarmModalContextProvider = ({ children }: FarmProviderProps) => {
    const [isEdit, setISEdit] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(false);
  
    return (
        <FarmModalContext.Provider value={{
            isEdit,
            setISEdit,
            modalIsOpen,
            setModalIsOpen
        }}>
            {children}
        </FarmModalContext.Provider>
    );
};
