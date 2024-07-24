import React from 'react'
import {useQuery} from "@tanstack/react-query";
import {getHealthCheck} from "../apiClient/healthCheck";

export const SampleHello: React.FC = () => {
    const { isPending, error, data } = useQuery({ queryKey: ['healthCheck'], queryFn: getHealthCheck })

    if (isPending) return 'Loading...'

    if (error) return 'An error has occurred: ' + error.message

    return (
        <>
          <div>backend health: {data?.data.message}</div>
        </>
    )
}