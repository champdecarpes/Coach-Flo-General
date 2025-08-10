import { ReactNode } from "react";
import { Stack } from "react-bootstrap";

// Interface for component props to type the children prop
interface MainLeftNavSideBarProps {
  children?: ReactNode;
}

export default function MainLeftNavSideBar({
  children,
}: MainLeftNavSideBarProps) {
  return (
    <Stack className="h-full">
      <div className="p-2">Test 1</div>
      <div className="p-2">Test 2</div>
      <div className="p-2 me-auto">Test 3</div>
      <div className="p-2">{children}</div>
    </Stack>
  );
}
