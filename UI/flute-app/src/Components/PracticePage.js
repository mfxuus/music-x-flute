// import React, { useState, useRef, useEffect } from 'react';
// import Button from 'react-bootstrap/Button';
// import Container from 'react-bootstrap/Container';
// import Row from 'react-bootstrap/Row';
// import Col from 'react-bootstrap/Col';

// import {Circle, Line} from 'react-shapes';
// import useWebSocket from 'react-use-websocket';



// import config from '../config.js';
// import FluteDemo from './FluteDemo.js';

// function PracticePage() {

//   const expectedRows = 6;
//   const [fluteRowHeight, setFluteRowHeight] = useState(0);
//   const [fingerPositions, setFingerPositions] = useState([]);
//   const [cursorPosition, setCursorPosition] = useState(0);
//   const [correctPositions, setCorrectPositions] = useState([]);
  
//   const [status, setStatus] = useState('not_started');
//   const {
//     sendMessage,
//     sendJsonMessage,
//     lastMessage,
//     lastJsonMessage,
//     readyState,
//     getWebSocket,
//   } = useWebSocket(config.websocketUrl, {
//     onOpen: () => {
//       console.log('opened')
//       sendMessage(JSON.stringify({path: 'tempo-practice', data: 'get-current-tempo'}))
//     },
//     shouldReconnect: (closeEvent) => true,
//   });


//   // Get element height to set cursor position
//   const ref = useRef(null);
//   useEffect(() => {
//     if (ref.current) {
//       setFluteRowHeight(ref.current.clientHeight);
//     }
//   }, [fingerPositions]);


//   const startTest = () => {
//     console.log('Starting Test')
//     sendMessage(JSON.stringify({path: 'test-phase', data: 'start_test'}))
//     setFingerPositions([]);
//     setCursorPosition(0);
//     setCorrectPositions([]);
//     setStatus('started')

//   }

//   useEffect(() => {
//     if (lastMessage !== null) {
//       console.log(lastMessage)
//       if (lastMessage.data === 'playback_complete') {
//         setStatus('playback_complete');
//         return
//       }
//       if (lastMessage.data === 'start') {
//         return
//       }
//       if (lastMessage.data === 'start_playback') {
//         setStatus('start_playback');
//         return
//       }
//       const data = JSON.parse(lastMessage.data);
//       if (data.fingerPositions) {
//         setFingerPositions(data.fingerPositions)
//       }
//       if (data.cursorPosition) {
//         setCursorPosition(data.cursorPosition)
//       }
//       if (data.correctPositions) {
//         setCorrectPositions(data.correctPositions)
//       }
//     }
//   }, [lastMessage]);

//   const renderEmptyFluteDemos = () => {
//     const rows = [];
//     for (let i = 0; i < expectedRows - fingerPositions.length; i++) {
//       rows.push(
//         <Row className="my-2" key={i}>
//           <Col xs={3} sm={2}></Col>
//           <Col xs={9} sm={10}>
//             <FluteDemo positions={null} />
//           </Col>
//         </Row>
//       );
//     }
//     console.log(fingerPositions)
//     console.log(rows)
//     return rows;
//   }


//   return (

//     <Container>
//       {!['start_playback', 'started'].includes(status) &&
//         <Row>
//           <Col>
//             <Button
//               className='dashboard-btn'
//               variant="primary"
//               onClick={() => {startTest()}}>
//               {status === 'playback_complete' ? 'Start Next Test' : 'Start Test'}
//             </Button>
//           </Col>
//           <Col>
//             <Button
//               className='dashboard-btn'
//               variant="primary"
//               onClick={() => {sendMessage(JSON.stringify({path: 'test-phase', data: 'reset'}))}}>
//               Reset Tests
//             </Button>
//           </Col>
//         </Row>
//       }

//       {status !== 'not_started' &&
//         <React.Fragment>
//           {fingerPositions.map((item, i) => (
//             <Row className="my-2" ref={ref} key={i}>
//               <Col xs={3} sm={2}>
//                 {i === (fingerPositions.length - 1) && status === 'start_playback' &&
//                   <Line
//                     x1={25} x2={100}
//                     y1={parseInt(fluteRowHeight*cursorPosition*0.85)}
//                     y2={parseInt(fluteRowHeight*cursorPosition*0.85)}
//                     stroke={{color:'#E65243'}} strokeWidth={3}
//                   />
//                 }
//               </Col>

//               <Col xs={9} sm={10}>
//                 <FluteDemo
//                   key={i}
//                   positions={item}
//                   status={
//                     i === (fingerPositions.length - 1) && (status === 'start_playback') ? 'active' : 'done'}
//                   correctPositions={correctPositions[i]}
//                 />
//               </Col>
//             </Row>
//           ))}

//           {renderEmptyFluteDemos()}

//         </React.Fragment>
//       }

//     </Container>
//   )
// }


// export default PracticePage;
