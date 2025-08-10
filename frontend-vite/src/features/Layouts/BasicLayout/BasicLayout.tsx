import React, { ReactNode } from "react";

import MainLeftNavSideBar from "src/features/Layouts/BasicLayout/MainLeftNavSideBar";

// Interface for component props to type the children prop
interface MainLeftNavSideBarProps {
  children: ReactNode;
}
export default function BasicLayout({ children }: MainLeftNavSideBarProps) {
  return (
    <>
      <MainLeftNavSideBar>
        <p>Test Test Test</p>
      </MainLeftNavSideBar>
      {children}
    </>
  );
}
