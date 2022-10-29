import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {Circle} from 'react-shapes';

import {serverWS, sendWsMsg} from '../api.js';


const FluteDemo = ({positions, status, correctPositions}) => {

  const getBackgroundColor = () => {
    if (status === 'active') {
      return '#b2dfb2';
    } else if (status === 'done') {
      return '#bbbbbb';
    } else {
      return 'white';
    }
  }

  return (
    <Row
      className="px-2 flute-row"
      style={{borderRadius: "4px", background: getBackgroundColor(), maxWidth: "160px", margin: "auto"}}
    >
      
      {(positions && positions.length > 0) && positions.map((item, i) => (
        <div key={i} style={{margin: "auto"}} className="my-3">
          <Circle r={24} fill={{color:item === 1 ? '#2409ba' : 'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          {correctPositions &&
            <Circle r={12} fill={{color: correctPositions.includes(i) ? 'green': 'white'}}
              stroke={{color:'#green'}} strokeWidth={3} />
          }
        </div>
      ))}
        
      {(!positions || positions.length === 0) &&
        <React.Fragment>
          <div className="my-3">
            <Circle r={24} fill={{color:'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          </div>
          <div className="my-3">
            <Circle r={24} fill={{color:'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          </div>
          <div className="my-3">
            <Circle r={24} fill={{color:'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          </div>
          <div className="my-3">
            <Circle r={24} fill={{color:'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          </div>
          <div className="my-3">
            <Circle r={24} fill={{color:'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          </div>
          <div className="my-3">
            <Circle r={24} fill={{color:'white'}} stroke={{color:'#2409ba'}} strokeWidth={3} />
          </div>
        </React.Fragment>
      }

    </Row>
  )
}

export default FluteDemo;