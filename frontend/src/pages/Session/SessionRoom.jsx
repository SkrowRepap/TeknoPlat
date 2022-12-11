import React, { useContext, useEffect, useState } from 'react'
import Navbar from '../../components/Navbar/Navbar'
import './sessionRoom.scss'
import Settings from '../../components/SessionRoom/Settings'
import Stream from '../../components/SessionRoom/Stream'
import { useHMSActions } from "@100mslive/react-sdk";
import Loading from '../../components/Loading/Loading'
import SessionContext from '../../context/SessionContext'
import useGetPeer from '../../hooks/useGetPeer'
import useNotification from '../../hooks/useNotification'
import Notification from '../../components/Notifcation/Notifcation'
import { Navigate } from 'react-router'

function SessionRoom() {
    const { session, dispatch } = useContext(SessionContext)
    const loading = session.loading
    const role = session.role

    const hmsActions = useHMSActions()
    const { isConnected } = useGetPeer({ role })
    const [loadingText, setloadingText] = useState('')
    const notification = useNotification()

    useEffect(() => {
        window.onunload = () => {
            if (isConnected) {
                hmsActions.leave();
                dispatch({ type: "LEAVE" })
            }
        };
    }, [hmsActions, isConnected]);

    useEffect(() => {
        const unSub = () => {
            if (role === 'creator' && session.loading === true) {
                setloadingText("We are now preparing your session...")
            }
            if (role === 'participant' && session.loading === true) {
                setloadingText("Waiting for host to enter the session...")
            }
        }

        return (
            unSub()
        )
    }, [role, session.loading, isConnected])


    return (
        <div className='main-content'>
            <Navbar />
            {isConnected ?
                loading === false ? (
                    <>
                        <div className='sessionRoom'>
                            <div className="sessionRoom-container">
                                <Settings role={role} />
                                <Stream role={role} />
                            </div>
                            <Notification />
                        </div>
                    </>) : (<Loading text={loadingText} />)
                : (
                    <>
                        <Navigate to={'/dashboard'} />
                    </>
                )
            }
        </div>

    )
}

export default SessionRoom
