import type { NextPage } from 'next';
import Uniai from '../../components/unias';
import styles from './Home.module.css';

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <main>
        <Uniai />
      </main>
    </div>
  );
}

export default Home;