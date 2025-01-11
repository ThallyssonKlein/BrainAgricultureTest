import { IFarm } from "../paginated_select/IFarmer";

interface AverageLandUse {
  average_arable_area: number;
  average_vegetation_area: number;
}

export default interface IData {
  farm_count: number;
  total_hectares: number;
  farm_counts_grouped_by_state: IFarm[];
  farms_grouped_by_state: IFarm[];
  farms_count_grouped_by_culture: IFarm[];
  farms_grouped_by_culture: IFarm[];
  average_land_use: AverageLandUse;
}