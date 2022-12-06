import { useHMSActions } from '@100mslive/react-sdk';
import React from 'react'

function SessionNav({ role, sessionID }) {
    const hmsActions = useHMSActions();

    const endRoom = async () => {
        try {
            const lock = false; // set to true to disallow rejoins
            const reason = 'party is over';
            await hmsActions.endRoom(lock, reason);
        } catch (error) {
            // Permission denied or not connected to room
            console.error(error);
        }
    };
    return (
        <div className='sessionNav-container'>
            <div className="sessionNav-controls">
                <div className="pitch-title">
                    <span>Pitch Title</span>
                </div>
                {role === 'creator' ? (
                    <div className="sessionNav-buttons">
                        <button className='askPro-button'>Ask a Pro</button>
                        <button className='uploadFiles-button'>Upload Files</button>
                        <button className='openRating-button'>Open Rating</button>
                    </div>
                ) : (null)
                }

            </div>
            {role === 'creator' ? (
                <div className="sessionNav-endSession">
                    <button onClick={endRoom}>End Session</button>
                </div>) : (null)
            }
        </div>
    )
}

export default SessionNav