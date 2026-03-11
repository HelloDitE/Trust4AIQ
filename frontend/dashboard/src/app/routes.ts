import { createBrowserRouter } from "react-router-dom";
import { ServiceOverview } from "./pages/ServiceOverview";
import { RoomDetail } from "./pages/RoomDetail";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: ServiceOverview,
    // element: <ServiceOverview />,
  },
  {
    path: "/rooms/:room_id",
    Component: RoomDetail,
    // element: <RoomDetail />,
  },
]);
