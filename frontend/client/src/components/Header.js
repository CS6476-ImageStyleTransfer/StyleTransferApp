import React from 'react'

export default (props) => (
  <header>
    <div className='category-wrapper'>
      <div className='category'>
        <span>Photo to Painting</span>
      </div> 
      <div className='choice-wrapper'>
        <button className='my-choice' onClick={props.setStyle}>Candy</button>
        <button className='my-choice' onClick={props.setStyle}>Mosaic</button>
        <button className='my-choice' onClick={props.setStyle}>RainPrincess</button>
        <button className='my-choice' onClick={props.setStyle}>Udnie</button>
      </div>
    </div>
    <div className='category-wrapper'>
      <div className='category'>
        <span>Photo to Cartoon</span>
      </div> 
      <div className='choice-wrapper'>
        <button className='my-choice' onClick={props.setStyle}>Hayao</button>
        <button className='my-choice' onClick={props.setStyle}>Hosoda</button>
        <button className='my-choice' onClick={props.setStyle}>Paprika</button>
        <button className='my-choice' onClick={props.setStyle}>Skinkai</button>
      </div>
    </div>
    <div className='category-wrapper'>
      <div className='category'>
        <span>Painting to Photo</span>
      </div> 
      <div className='choice-wrapper'>
        <button className='my-choice' onClick={props.setStyle}>Monet</button>
        <button className='my-choice' onClick={props.setStyle}>Vangogh</button>
        <button className='my-choice' onClick={props.setStyle}>Ukiyoe</button>
        <button className='my-choice' onClick={props.setStyle}>Cezanne</button>
      </div>
    </div>
    <div className='category-wrapper'>
      <div className='category'>
        <span>Hand-drawn to Photo</span>
      </div> 
      <div className='choice-wrapper'>
        <button className='my-choice' onClick={props.setStyle}>Shoe</button>
        <button className='my-choice' onClick={props.setStyle}>Handbag</button>
        <button className='my-choice' onClick={props.setStyle}>Facade</button>
        <button className='my-choice' onClick={props.setStyle}>Map</button>
      </div>
    </div>
  </header>
)