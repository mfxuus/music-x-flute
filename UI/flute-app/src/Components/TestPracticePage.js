import React, { useState, useRef, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import {Circle, Line} from 'react-shapes';
import useWebSocket from 'react-use-websocket';



import config from '../config.js';
import FluteDemo from './FluteDemo.js';

function TestPracticePage({pageMode}) {

  const expectedRows = 6;

  const [fluteColWidth, setFluteColWidth] = useState(0);
  const [fingerPositions, setFingerPositions] = useState([]);
  const [cursorPosition, setCursorPosition] = useState(0);
  const [correctPositions, setCorrectPositions] = useState([]);
  const [currentPhase, setCurrentPhase] = useState('');
  const [currentTempo, setCurrentTempo] = useState(null);
  const [tempoStatus, setTempoStatus] = useState(null);
  
  
  const [status, setStatus] = useState('not_started');
  const {
    sendMessage,
    sendJsonMessage,
    lastMessage,
    lastJsonMessage,
    readyState,
    getWebSocket,
  } = useWebSocket(config.websocketUrl, {
    onOpen: () => {
      console.log('opened')
      sendMessage(JSON.stringify({path: 'tempo', data: 'get-current-tempo'}))
    },
    shouldReconnect: (closeEvent) => true,
  });


  // Get element width to set cursor position
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) {
      setFluteColWidth(ref.current.clientWidth);
    }
  }, [fingerPositions]);


  useEffect(() => {
    console.log(currentPhase)
    sendMessage(JSON.stringify({path: 'change-phase', data: currentPhase}))
  }, [currentPhase]);


  const startTest = () => {
    console.log('Starting')
    if (pageMode === 'test') {
      sendMessage(JSON.stringify({path: 'test-practice', data: 'start_test'}))
    } else {
      sendMessage(JSON.stringify({path: 'test-practice', data: 'start_practice'}))
    }
    setFingerPositions([]);
    setCursorPosition(0);
    setCorrectPositions([]);
    setStatus('started')
  }

  const changeTempo = (dir) => {
    sendMessage(JSON.stringify({path: 'tempo', data: dir}))
  }

  useEffect(() => {
    if (lastMessage !== null) {
      console.log(lastMessage)
      if (['playback_complete', 'start_playback', 'phase_complete'].includes(lastMessage.data)) {
        setStatus(lastMessage.data);
        return
      }
      if (lastMessage.data === 'start') {
        return
      }
      if (['tempo-max', 'tempo-min', 'tempo-ok'].includes(lastMessage.data)) {
        setTempoStatus(lastMessage.data);
        return
      }
      const data = JSON.parse(lastMessage.data);
      if (data.fingerPositions) {
        setFingerPositions(data.fingerPositions)
      }
      if (data.cursorPosition) {
        setCursorPosition(data.cursorPosition)
      }
      if (data.correctPositions) {
        setCorrectPositions(data.correctPositions)
      }
      if (data.currentTempo) {
        setCurrentTempo(data.currentTempo)
      }
    }
  }, [lastMessage]);

  const renderEmptyFluteDemos = () => {
    const cols = [];
    for (let i = 0; i < expectedRows - fingerPositions.length; i++) {
      cols.push(
        <Col className="my-2" key={i} xs={2}>
          <div style={{height: "128px"}}></div>
          <FluteDemo positions={null} />
        </Col>
      );
    }
    console.log(fingerPositions)
    console.log(cols)
    return cols;
  }

  const getMainBtnText = () => {
    let res
    if (pageMode === 'test') {
      res = status === 'playback_complete' ? 'Start Next Test' : 'Start Test'
    } else {
      res = status === 'playback_complete' ? 'Re-Start Practice' : 'Start Practice'
    }
    return res
  }


  return (

    <Container fluid='lg'>
      {!['start_playback', 'started', 'phase_complete'].includes(status) &&
        <Row>
          <Col>
            <Button
              className='dashboard-btn'
              variant="primary"
              disabled={pageMode==='test' && currentPhase===''}
              onClick={() => {startTest()}}>
              {getMainBtnText()}
            </Button>
          </Col>
          
          {pageMode === 'test' &&
            <Col>
              <Button
                className='dashboard-btn'
                variant="primary"
                onClick={() => {sendMessage(JSON.stringify({path: 'test-practice', data: 'reset'}))}}>
                Reset Tests
              </Button>
            </Col>
          }

          {pageMode === 'test' &&
            <Col>
              <Form.Select
                  size="md"
                  value={currentPhase}
                  onChange={(e) => setCurrentPhase(e.target.value)}
                  >
                <option disabled={currentPhase !== ''}>Select Phase</option>
                <option value='phase-1'>Phase 1</option>
                <option value='phase-2'>Phase 2</option>
                <option value='phase-3'>Phase 3</option>
              </Form.Select>
            </Col>
          }

          {pageMode === 'practice' &&
            <Col>
              <Row>
                <Col>
                  <Button
                    className='dashboard-btn'
                    variant="primary"
                    disabled={tempoStatus === 'tempo-min'}
                    onClick={() => changeTempo('decrease')}>
                    Tempo -
                  </Button>
                </Col>
                <Col>
                  <Button
                    className='dashboard-btn'
                    variant="primary"
                    disabled={tempoStatus === 'tempo-max'}
                    onClick={() => changeTempo('increase')}>
                    Tempo +
                  </Button>
                </Col>
              </Row>
            </Col>
          }
        </Row>
      }

      {status === 'phase_complete' &&
        <Row>
          <Col>
            <h5>You have completed this phase.</h5>
            {(currentPhase === 'phase-1' || currentPhase === 'phase-2') ?
              <p>Please move on to the next phase.</p>
              :
              <p>Thank you!</p>
            }
          </Col>
        </Row>
      }

      {status !== 'not_started' &&
        <Row>
          {fingerPositions.map((item, i) => (
            <Col className="my-2" ref={ref} key={i} xs={2}>
              <div style={{height: "128px"}}>
                {i === (fingerPositions.length - 1) && status === 'start_playback' &&
                  <Line
                    y1={25} y2={100}
                    x1={parseInt(fluteColWidth*cursorPosition*0.75)}
                    x2={parseInt(fluteColWidth*cursorPosition*0.75)}
                    stroke={{color:'#E65243'}} strokeWidth={3}
                  />
                }
              </div>

              <FluteDemo
                key={i}
                positions={item}
                status={
                  i === (fingerPositions.length - 1) && (status === 'start_playback') ? 'active' : 'done'}
                correctPositions={correctPositions[i]}
              />
            </Col>
          ))}

          {renderEmptyFluteDemos()}

        </Row>
      }


    </Container>
  )
}


export default TestPracticePage;
