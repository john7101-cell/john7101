import React from "react";
import { Composition } from "remotion";
import { Edit, DUR } from "./Edit";
export const Root: React.FC = () => (
  <Composition id="Edit" component={Edit} width={1080} height={1920} fps={30} durationInFrames={Math.round(DUR * 30)} />
);
