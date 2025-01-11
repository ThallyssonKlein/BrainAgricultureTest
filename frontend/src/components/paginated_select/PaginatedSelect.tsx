import React, { useState, useEffect, useRef, useContext } from 'react';
import './PaginatedSelect.css';
import IFarmer from '../IFarmer';
import API from '../../API';
import { OptionsContext } from '../../context/OptionsContext';

export const PaginatedSelect: React.FC = () => {
  const { selectedOption, setSelectedOption, options, setOptions, setSelectedObject } = useContext(OptionsContext)
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement | null>(null);

  const fetchOptions = async (page: number, searchTerm: string): Promise<IFarmer[]> => {
    const response = await API.get(`/api/v1/farmer?page=${page}&limit=10&query=${searchTerm}`);

    if (response.status !== 200) {
      alert('Error fetching farmers!');
    }

    return (response.data as IFarmer[]);
  };
    
  const loadOptions = async (page: number, searchTerm: string) => {
    setIsLoading(true);
    const newOptions: IFarmer[] = await fetchOptions(page, searchTerm);
    if (newOptions.length === 0) {
      setHasMore(false);
    } else {
      setOptions([...options, ...newOptions]);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    if (isOpen) {
      loadOptions(page, searchTerm);
    }
  }, [page, searchTerm, isOpen]);

  const handleScroll = () => {
    if (!dropdownRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } = dropdownRef.current;
    if (scrollTop + clientHeight >= scrollHeight - 10 && hasMore && !isLoading) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setOptions([]); 
    setPage(1);
    setHasMore(true);
  };

  const handleDropdownClick = () => {
    setIsOpen((prevIsOpen) => !prevIsOpen);
    if (!isOpen) {
      setOptions([]);
      setPage(1);
      setHasMore(true);
    }
  };

  const handleOptionClick = (name: string, id: number) => {
    setSelectedOption(id);
    setSelectedObject(options.find(option => option.id === id));
    setSearchTerm(name);
    setTimeout(() => setIsOpen(false), 100)
  };

  return (
    <div className="paginated-select">
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-input"
        onClick={handleDropdownClick}
      />
      {isOpen && (
        <div
          className="options-dropdown"
          ref={dropdownRef}
          onScroll={handleScroll}
          role="listbox"
        >
          {options.map((option, index) => (
            <div
              key={index}
              className={`option-item ${selectedOption === option.name ? 'selected' : ''}`}
              onClick={() => handleOptionClick(option.name, option.id)}
            >
              {option.name}
            </div>
          ))}
          {isLoading && <div className="loading">Loading...</div>}
          {!hasMore && <div className="no-more">No more options</div>}
        </div>
      )}
    </div>
  );
};