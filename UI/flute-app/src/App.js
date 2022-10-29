import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import './App.scss';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import TestPracticePage from './Components/TestPracticePage.js';

function App() {

  const [currentSection, setCurrentSection] = useState('dashboard');

  useEffect(() => {
    document.title = "Flute App"
  }, []);

  return (
    <div className="App">

      <Navbar bg="light" expand="lg">
        <Container>
          <Navbar.Brand href="#home">Flute App</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          {currentSection !== 'dashboard' &&
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link
                  className={currentSection==='dashboard' ? 'active' : ''}
                  onClick={() => {setCurrentSection('dashboard')}}>
                  Home
                </Nav.Link>
                <Nav.Link
                  className={currentSection==='practice' ? 'active' : ''}
                  onClick={() => {setCurrentSection('practice')}}>
                  Practice
                </Nav.Link>
                <Nav.Link
                  className={currentSection==='test' ? 'active' : ''}
                  onClick={() => {setCurrentSection('test')}}>
                  Test
                </Nav.Link>
                <Nav.Link
                  className={currentSection==='learn' ? 'active' : ''}
                  onClick={() => {setCurrentSection('learn')}}>
                  Learn
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          }
        </Container>
      </Navbar>

      {currentSection === 'dashboard' &&
        <Container className='dashboard-container'>
          <Row>
            <Col xs={4} className='offset-sm-4'>
              <Button
                className='dashboard-btn'
                variant="primary"
                onClick={() => {setCurrentSection('practice')}}>
                Practice
              </Button>
            </Col>
          </Row>
          <Row>
            <Col xs={4} className='offset-sm-4'>
              <Button
                className='dashboard-btn'
                variant="primary"
                onClick={() => {setCurrentSection('test')}}>
                Test
              </Button>
            </Col>
          </Row>
          <Row>
            <Col xs={4} className='offset-sm-4'>
              <Button
                className='dashboard-btn'
                variant="primary"
                onClick={() => {setCurrentSection('learn')}}>
                Learn
              </Button>
            </Col>
          </Row>
        </Container>
      }

      {currentSection === 'test' &&
        <TestPracticePage pageMode='test' />
      }

      {currentSection === 'practice' &&
        <TestPracticePage pageMode='practice' />
      }



    </div>
  );
}

export default App;
