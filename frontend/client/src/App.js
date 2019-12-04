import React, { Component } from 'react'
import Notifications, { notify } from 'react-notify-toast'
import Spinner from './components/Spinner'
import UploadImage from './components/UploadImage'
import ResultImage from './components/ResultImage'
import UploadButton from './components/UploadButton'
import Cover from './components/Cover'
import Header from './components/Header'
import Footer from './components/Footer'
import { IMAGE_SERVER_URL, TRANSFORM_SERVER_URL } from './config'
import './App.css'

const toastColor = { 
  background: '#505050', 
  text: '#ffffff' 
}

export default class App extends Component {
  
  state = {
    uploading: false,
    transforming: false,
    images: [],
    result: '',
    style: ''
  }

  toast = notify.createShowQueue()

  onUploadImage = e => {
    const errs = [] 
    const files = Array.from(e.target.files)

    if (files.length > 1) {
      const msg = 'Only 1 image can be uploaded at a time'
      return this.toast(msg, 'custom', 2000, toastColor)  
    }

    const formData = new FormData()
    const types = ['image/png', 'image/jpeg', 'image/gif']

    files.forEach((file, i) => {
      if (types.every(type => file.type !== type)) {
        errs.push(`'${file.type}' is not a supported format`)
      }

      if (file.size > 50000000) {
        errs.push(`'${file.name}' is too large, please pick a smaller file`)
      }

      formData.append(i, file)
    })

    if (errs.length) {
      return errs.forEach(err => this.toast(err, 'custom', 2000, toastColor))
    }

    this.setState({ uploading: true })

    fetch(`${IMAGE_SERVER_URL}/image-upload`, {
      method: 'POST',
      body: formData
    })
    .then(res => {
      if (!res.ok) {
        throw res
      }
      return res.json()
    })
    .then(images => {
      this.setState({
        uploading: false, 
        images
      })
    })
    .catch(err => {
      err.json().then(e => {
        this.toast(e.message, 'custom', 2000, toastColor)
        this.setState({ uploading: false })
      })
    })
  }

  filter = id => {
    return this.state.images.filter(image => image.public_id !== id)
  }

  removeImage = id => {
    this.setState({ 
      images: this.filter(id),
      result: ''
    })
  }

  onError = id => {
    this.toast('Oops, something went wrong', 'custom', 2000, toastColor)
    this.setState({ images: this.filter(id) })
  }

  transformStyle = () => {
    if (this.state.images.length === 0) {
      const msg = 'Please upload an image first!' 
      this.toast(msg, 'custom', 2000, toastColor)
    } else if (this.state.style.length === 0) {
      const msg = 'Please select a style first!' 
      this.toast(msg, 'custom', 2000, toastColor)
    } else {
      const url = this.state.images[0].secure_url
      const chosenStyle = this.state.style
      this.setState({transforming: true})
      fetch(`${TRANSFORM_SERVER_URL}/tf`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          "Access-Control-Allow-Origin": "*",
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'img_url': url,
          'style': chosenStyle
        })
      })
      .then(res => {
        res.json().then(resJson => {
          this.setState({
            result: resJson['img_url'],
            transforming: false
          })
        })
      })
      .catch(err => {
        err.json().then(e => {
          this.toast(e.message, 'custom', 2000, toastColor)
          this.setState({ transforming: false })
        })
      })
    }
  }

  setStyle = e => {
    const chosenStyle = e.target.innerHTML
    this.setState({ style: chosenStyle })
    const choices = document.getElementsByClassName('clicked')
    if (choices.length > 0) {
      choices[0].className = 'my-choice'
    }
    e.target.classList.add('clicked')
  }
  
  render() {
    const { uploading, images, result, transforming } = this.state
    
    const leftContent = () => {
      switch(true) {
        case uploading:
          return <Spinner />
        case images.length > 0:
          return <UploadImage
                  images={images} 
                  removeImage={this.removeImage} 
                  onError={this.onError}
                 />
        default:
          return <UploadButton onChange={this.onUploadImage} />
      }
    }

    const rightContent = () => {
      switch(true) {
        case transforming: 
          return <Spinner />
        case result.length > 0:
          return <ResultImage image={result} />
        default:
          return <Cover />
      }
    }

    const content = () => {
      return (
        <main className='content'>
          <div className='left-container'>
            {leftContent()}
          </div>
          <div className='middle-container'>
            <button className="my-button" onClick={this.transformStyle}>TRANSFORM</button>
          </div>
          <div className='right-container'>
            {rightContent()}
          </div>
        </main>
      )
    }

    return (
      <div className='container'>
        <Notifications />
        <Header setStyle={this.setStyle} />
        {content()}
        <Footer />
      </div>
    )
  }
}