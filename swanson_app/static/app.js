'use strict';

const e = React.createElement;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
        liked: false,
        error: null,
        isLoaded: false,
        items: []
    };
  }

  componentDidMount() {
    const proxyurl = "https://cors-anywhere.herokuapp.com/";
    const url = "https://hello-swanson.herokuapp.com/api/quote";
    const url2 = "https://127.0.0.1:5000/api/data";
    fetch(url)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result // was result.items, referencing data.json
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }
  
  
  render() {
    const { error, isLoaded, items } = this.state;
    console.log(this.state.items.note);
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
        return (
            <div className="quote-box">
                <h2>{ items.quote }</h2>
                <h4>- { items.author }</h4>
                <h4> {items.word_count}</h4>
                <h4>Rating: 5 / 5</h4>
                <button onClick={() => {this.componentDidMount(); this.setState({isLoaded: false});}}>
                    Click here to get a random quote!
                </button>
                <br />
                <button onClick={() => {this.setState({isLoaded: false}); this.callBig();}}>
                Big Quote
                </button>
                <button onClick={() => {this.setState({isLoaded: false}); this.callMed();}}>
                Medium Quote
                </button>
                <button onClick={() => {this.setState({isLoaded: false}); this.callSmall();}}>
                Small Quote
                </button>
            </div>
            
        );
      }
    
    // if (this.state.liked) {
    //   return 'You liked this.';
    // }

    // // Display a "Like" <button>
    // return (
    //     <button onClick={() => this.setState({ liked: true })}>
    //         Get a quote!
    //     </button>
    // );
  }
}

const domContainer = document.querySelector('#app');
ReactDOM.render(e(App), domContainer);