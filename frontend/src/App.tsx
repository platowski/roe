import React from "react"
import './App.css'
import {SampleHello} from "./components/SampleHello";
import {queryClient} from "./apiClient/queryClient";
import {QueryClientProvider} from "@tanstack/react-query";

export const App: React.FC = () => {


  return (
    <>
        <QueryClientProvider client={queryClient}>
            <h1>Sample App Boilerplate</h1>
            <SampleHello />
        </QueryClientProvider>
    </>
  )
}
