import React, { Component } from 'react'
import Notifications, { notify } from 'react-notify-toast'
import Spinner from './components/Spinner'
import UploadImage from './components/UploadImage'
import ResultImage from './components/ResultImage'
import Button from './components/Button'
import Cover from './components/Cover'
import WakeUp from './components/WakeUp'
import Footer from './components/Footer'
import { API_URL } from './config'
import './App.css'

const toastColor = { 
  background: '#505050', 
  text: '#ffffff' 
}

export default class App extends Component {
  
  state = {
    loading: true,
    uploading: false,
    images: [],
    result: []
  }

  componentDidMount() {
    fetch(`${API_URL}/wake-up`)
      .then(res => {
        if (res.ok) {
          return this.setState({ loading: false })  
        }
        const msg = 'Something is went wrong with image server' 
        this.toast(msg, 'custom', 2000, toastColor)
      })
  }

  toast = notify.createShowQueue()

  onChange = e => {
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

    fetch(`${API_URL}/image-upload`, {
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
    this.setState({ images: this.filter(id) })
  }

  onError = id => {
    this.toast('Oops, something went wrong', 'custom', 2000, toastColor)
    this.setState({ images: this.filter(id) })
  }
  
  render() {
    const { loading, uploading, images, result } = this.state
    
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
          return <Button onChange={this.onChange} />
      }
    }

    const rightContent = () => {
      switch(true) {
        case result.length > 0:
          return <ResultImage />
        default:
          return <Cover />
      }
    }

    const content = () => {
      switch(true) {
        case loading:
          return (
            <div className='content'>
              <WakeUp />
            </div>
          )
        default:
          return (
            <div className='content'>
              <div className='left-container'>
                {leftContent()}
              </div>
              <div className='right-container'>
                {rightContent()}
              </div>
            </div>
          )
      }
    }

    return (
      <div className='container'>
        <Notifications />
        {content()}
        <Footer />
      </div>
    )
  }
}